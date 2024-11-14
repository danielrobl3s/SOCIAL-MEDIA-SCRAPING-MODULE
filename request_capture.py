from mitmproxy import ctx
import json

class RequestCapture:
    def __init__(self):
        self.captured_requests = []
    
    def request(self, flow):
        request_data = {
            'url': flow.request.pretty_url,
            'method': flow.request.method,
            'headers': dict(flow.request.headers),
            'params': dict(flow.request.query),
        }
        
        if flow.request.method == 'POST' and flow.request.content:
            try:
                request_data['post_data'] = flow.request.get_text()
            except:
                request_data['post_data'] = str(flow.request.content)
        
        self.captured_requests.append(request_data)
        
        with open('params.json', 'w') as f:
            json.dump(self.captured_requests, f, indent=2)

addons = [RequestCapture()]