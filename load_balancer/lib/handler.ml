open Lwt.Syntax

type status = Healthy | Dead
let servers = [|
  "http://localhost:3500";
  "http://localhost:3501";
  "http://localhost:3502";
|]
let statuses = Array.map (fun _ -> Healthy) servers

let req_idx = ref 0
let get_server () =
  if (not (Array.exists (fun status -> status = Healthy) statuses))
  then failwith "no healthy instances"
  else
    while statuses.(!req_idx) = Dead do
      req_idx := (!req_idx + 1) mod (Array.length servers)
    done;
    let res = servers.(!req_idx) in
    req_idx := (!req_idx + 1) mod (Array.length servers);
    res


let is_server_healthy (server : string) =
  let http_promise = Cohttp_lwt_unix.Client.get (Uri.of_string server) in
  let is_ok (resp, _) = (resp |> Cohttp_lwt_unix.Response.status |> Cohttp.Code.code_of_status) = 200 in
  try%lwt
    Lwt.map is_ok http_promise
  with
    | exn -> Lwt.return false

let rec healthcheck () =
  let* () = Lwt_unix.sleep 5. in
  for i = 0 to (Array.length servers) - 1 do
    let _ =
      let promise = is_server_healthy servers.(i) in
      let get_status is_ok = if is_ok then Healthy else Dead in
      let update_status is_ok = 
        statuses.(i) <- (get_status is_ok);
        Printf.eprintf "Server %s ok=%b\n" servers.(i) is_ok;
      in
      Lwt.map update_status promise
    in ()
  done;
  healthcheck ()
    
  
let handle _ = 
  let server = get_server () in
  let%lwt (resp, body) = Cohttp_lwt_unix.Client.get (Uri.of_string server) in 
  let () = Printf.eprintf "Response code: %d\n" (resp |> Cohttp_lwt_unix.Response.status |> Cohttp.Code.code_of_status);
  Printf.eprintf "Headers: %s\n" (resp |> Cohttp_lwt_unix.Response.headers |> Cohttp.Header.to_string) in
  let%lwt body_string = (body |> Cohttp_lwt.Body.to_string) in
    (* Printf.eprintf "Body: %s\n" body_string; *)
    Dream.empty `OK
