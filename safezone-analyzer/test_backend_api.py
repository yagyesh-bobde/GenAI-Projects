import httpx
import asyncio

async def test_api():
    base_url = "http://localhost:8000"

    print(f"--- Testing Backend API at {base_url} ---")

    # 1. Test Health
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{base_url}/health")
            print(f"Health check: {resp.status_code} -> {resp.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return

    # 2. Test Analysis Trigger
    try:
        async with httpx.AsyncClient() as client:
            print("\nTriggering analysis for 'test_repo'...")
            resp = await client.post(
                f"{base_url}/analyze",
                json={"repo_url": "test_repo"}
            )
            if resp.status_code != 200:
                print(f"Failed to trigger analysis: {resp.text}")
                return

            analysis_id = resp.json()["analysis_id"]
            print(f"Analysis started. ID: {analysis_id}")

            # 3. Poll for results
            print("Polling for results (this may take a few seconds)...")
            for _ in range(20):
                await asyncio.sleep(2)
                resp = await client.get(f"{base_url}/analyze/{analysis_id}")
                res_json = resp.json()
                status = res_json.get("status", "unknown")
                print(f"Status: {status}")

                if status == "completed":
                    print("Analysis Complete!")
                    data = res_json.get("data", {})
                    print(f"Summary: {data.get('summary')}")
                    break
                elif status == "failed":
                    print("Analysis Failed!")
                    break
            else:
                print("Polling timed out.")

    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
