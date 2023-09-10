import sys
from typing import Any
from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1
from datetime import datetime
import pytz

def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 600
) -> Any:
    result = operation.result(timeout=timeout)
    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)
    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)
    return result

def stop_instance(project_id: str, zone: str, instance_name: str) -> None:
    instance_client = compute_v1.InstancesClient()
    operation = instance_client.stop(
        project=project_id, zone=zone, instance=instance_name
    )
    wait_for_extended_operation(operation, "instance stopping")
    return

def start_instance(project_id: str, zone: str, instance_name: str) -> None:
    instance_client = compute_v1.InstancesClient()
    operation = instance_client.start(
        project=project_id, zone=zone, instance=instance_name
    )
    wait_for_extended_operation(operation, "instance start")
    return

def start_point(request):
    tz_KK = pytz.timezone('Asia/Saigon') 
    datetime_KK= datetime.now(tz_KK)
    print("Vietnam:", datetime_KK.strftime("%m/%d/%Y, %H:%M:%S"))
    hr = datetime_KK.hour
    mn = datetime_KK.minute
    if hr == 19 and mn == 5:
        print('It is 19:05. stopping vm now...')
        stop_instance("PROJECT_ID","ZONE","VM_NAME")
        return "Stopped VM...."
    elif hr == 7 and mn == 55:
        print('It is 7:55am. starting vm now...')
        start_instance("PROJECT_ID","ZONE","VM_NAME")
        return "Started VM...."
    else:
        print(hr)
        print("You should not manage VMs at these hours!!")
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S %z")