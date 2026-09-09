let handle _ = 
  let%lwt (resp, body) = Cohttp_lwt_unix.Client.get (Uri.of_string "https://example.com") in 
  let () = Printf.eprintf "Response code: %d\n" (resp |> Cohttp_lwt_unix.Response.status |> Cohttp.Code.code_of_status);
  Printf.eprintf "Headers: %s\n" (resp |> Cohttp_lwt_unix.Response.headers |> Cohttp.Header.to_string) in
  let%lwt body_string = (body |> Cohttp_lwt.Body.to_string) in
    Printf.eprintf "Body: %s\n" body_string;
    Dream.empty `OK
