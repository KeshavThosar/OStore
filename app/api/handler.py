class EndpointHandler:
  def __init__(self, endpoints = {}):
    self.endpoints = endpoints
    
  def handle_endpoint(self, endpoint):
    if endpoint in self.endpoints:
      handler = self.endpoints[endpoint]
      if handler is not None:
        return handler()
    return 'OK' #Need to add empty response or some error
    
