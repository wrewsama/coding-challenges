let () =
  Lwt.async Load_balancer.Handler.healthcheck;
  Dream.run
  @@ Dream.logger
  @@ Load_balancer.Handler.handle
