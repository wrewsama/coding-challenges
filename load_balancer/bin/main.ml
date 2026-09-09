let () =
  Dream.run
  @@ Dream.logger
  @@ Load_balancer.Handler.handle
