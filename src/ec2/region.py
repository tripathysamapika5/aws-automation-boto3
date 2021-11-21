class ServiceRegion:
    def __init__(self, 
                 service_region_name, 
                 service_region_endpoint
                ):
        self.service_region_name = service_region_name
        self.service_region_endpoint = service_region_endpoint
        
    def __str__(self):
        return """Details of ServiceRegion 
                service_region_name = {},
                service_region_endpoint = {}
              """.format(
                  self.service_region_name,
                  self.service_region_endpoint
                  )
