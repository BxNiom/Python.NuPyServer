class Services:
    _services = []

    def add_service(self, serviceId, serviceType):
        self._services.append({
            "@id": serviceId,
            "@type": serviceType
        })

    def create_index(self):
        return {
            "version": "3.0.0",
            "resources": self._services
        }
