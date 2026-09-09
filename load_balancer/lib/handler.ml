let servers = [
  "http://localhost:3500";
  "http://localhost:3501";
  "http://localhost:3502";
]
let req_idx = ref 0
let get_server () =
  req_idx := (!req_idx + 1) mod (List.length servers);
  List.nth servers !req_idx
  
  
let handle _ = 
  let server = get_server () in
  let%lwt (resp, body) = Cohttp_lwt_unix.Client.get (Uri.of_string server) in 
  let () = Printf.eprintf "Response code: %d\n" (resp |> Cohttp_lwt_unix.Response.status |> Cohttp.Code.code_of_status);
  Printf.eprintf "Headers: %s\n" (resp |> Cohttp_lwt_unix.Response.headers |> Cohttp.Header.to_string) in
  let%lwt body_string = (body |> Cohttp_lwt.Body.to_string) in
    Printf.eprintf "Body: %s\n" body_string;
    Dream.empty `OK
