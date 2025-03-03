
import requests
import json

private_token = "https://raw.githubusercontent.com/GBreen2/greentree/refs/heads/main/jtoken.json"

def handle_request(uid, server_name):
    url = f"https://like-api-of-chx.vercel.app/like?uid={uid}&server_name={server_name}&token={private_token}"
    
    try:
        response = requests.get(url, verify=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'message': 'API Server Not Responding',
            'http_code': response.status_code if response else None,
            'error': str(e)
        }

    try:
        res = response.json()
    except json.JSONDecodeError as e:
        return {
            'status': 'error',
            'message': 'Invalid JSON format',
            'error': str(e)
        }

    if 'status' in res:
        if res['status'] == "Success":
            return {
                'status': 'success',
                'message': 'System Access Granted',
                'data': res
            }
        else:
            return {
                'status': 'error',
                'message': 'System Access Denied',
                'response': res
            }
    else:
        return {
            'status': 'error',
            'message': 'Invalid API Response',
            'response': response.text
        }

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(json.dumps({
            'status': 'error',
            'message': 'Unauthorized Access',
            'error_code': 404
        }))
        sys.exit(1)

    uid = sys.argv[1]
    server_name = sys.argv[2]

    result = handle_request(uid, server_name)
    print(json.dumps(result, indent=4))
