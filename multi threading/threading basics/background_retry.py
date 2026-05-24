"""
In FastAPi application
The flow is receive Webhook -> Processing function -> Callback using httpx
Problem: The Callback can fail as the receiving callback services are down
Infra: It runs on k8s with 4 pods, postgres sql,
Data : The data i.e what payload and which url is saved in callback table
Approach: create a background worker for retry
1. callback fails -> A background worker retries it after 1 second -> timeout will be 10 seconds if it fails retry it for 3 times like after 5 and 10 seconds
2.Is it feasible or are there any better approaches ?
3.This should not impact memory in such way that it can cause crashes
"""
