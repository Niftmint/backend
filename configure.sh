clear
error_exit()
{
    echo "$1" 1>&2
    exit 1
}
echo configure:
echo
gcloud functions deploy info --runtime python39 --trigger-http --allow-unauthenticated || \
    error_exit "Error deploying function: info"
echo
echo
gcloud functions deploy create_link_token --runtime python39 --trigger-http --allow-unauthenticated || \
    error_exit "Error deploying function: create_link_token"
echo
echo
gcloud functions deploy set_access_token --runtime python39 --trigger-http --allow-unauthenticated || \
    error_exit "Error deploying function: set_access_token"
echo
echo
gcloud functions deploy auth --runtime python39 --trigger-http --allow-unauthenticated || \
    error_exit "Error deploying function: auth"
echo
echo
gcloud functions deploy identity --runtime python39 --trigger-http --allow-unauthenticated || \
    error_exit "Error deploying function: identity"
echo
echo
gcloud functions deploy balance --runtime python39 --trigger-http --allow-unauthenticated || \
    error_exit "Error deploying function: balance"
echo
echo done
echo
