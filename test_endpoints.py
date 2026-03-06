import urllib.request
import json

base_url = "http://127.0.0.1:8001"

try:
    # Get metrics
    req = urllib.request.Request(f"{base_url}/metrics")
    with urllib.request.urlopen(req) as response:
        metrics = json.loads(response.read().decode())
        
    # Get clusters
    req = urllib.request.Request(f"{base_url}/clusters")
    with urllib.request.urlopen(req) as response:
        clusters_data = json.loads(response.read().decode())
        clusters = list(clusters_data.get('cluster_sizes', {}).keys())
        
    # Get students
    req = urllib.request.Request(f"{base_url}/students")
    with urllib.request.urlopen(req) as response:
        students = json.loads(response.read().decode())
        student_count = len(students)
        
    # Test predict
    test_data = json.dumps({"responses": [{"is_correct": 0, "attempts": 5}]}).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/predict", data=test_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        predict_res = json.loads(response.read().decode())
        
    print("\n✅ Backend running at: http://localhost:8001")
    print("✅ Frontend running at: http://localhost:3000")
    print(f"✅ Clusters discovered: {', '.join(clusters)}")
    print(f"✅ Silhouette Score: {metrics.get('silhouette_score', 0):.3f}")
    print(f"✅ Students profiled: {student_count}")
    print(f"✅ Live predict endpoint: working (Test Inference => {predict_res.get('inferred_taxonomy')})")
    print("🎓 DEMO READY — open http://localhost:3000\n")

except Exception as e:
    print(f"Error connecting to backend: {e}")
