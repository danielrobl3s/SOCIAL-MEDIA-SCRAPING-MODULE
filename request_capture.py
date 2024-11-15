from mitmproxy import ctx
import json

class RequestCapture:
    def __init__(self):
        self.captured_requests = []
    
    def request(self, flow):
        # Capture request details
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
        
        # Store initial request data
        flow.request_data = request_data
    
    def response(self, flow):
        # Capture response details
        response_data = {
            'status_code': flow.response.status_code,
            'headers': dict(flow.response.headers),
        }
        
        try:
            response_data['content'] = flow.response.get_text()
        except:
            response_data['content'] = str(flow.response.content)
        
        # Combine request and response data
        full_data = flow.request_data
        full_data['response'] = response_data
        
        self.captured_requests.append(full_data)
        
        # Write to params.json
        with open('params.json', 'w') as f:
            json.dump(self.captured_requests, f, indent=2)

addons = [RequestCapture()]
