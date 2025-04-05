class ApiEndPoint(object):
    create_docker_repo = "/artifactory/api/repositories/docker-local"
    verify_docker_repo = "/artifactory/api/repositories"
    create_security_policy = "/xray/api/v2/policies"
    create_watch = "/xray/api/v2/watches"
    check_scan_status = "/xray/api/v1/artifact/status"
    verify_violations = "/xray/api/v1/violations"
