import requests

def get_real_shops(lat, lon):
    query = f"""
    [out:json];
    (
      node["shop"~"agrarian|tractor|hardware"](around:50000,{lat},{lon});
    );
    out center;
    """
    url = 'http://overpass-api.de/api/interpreter'
    try:
        response = requests.post(url, data={'data': query})
        data = response.json()
        print(len(data['elements']))
        if data['elements']:
            print(data['elements'][0])
    except Exception as e:
        print(e)
        
get_real_shops(11.0168, 76.9558)
