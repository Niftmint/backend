if [ $# -eq 0 ]; then
    echo
    echo "specify the URL of the file to your github to download"
    echo
    exit 1
fi

TOKEN='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'

echo
echo downloading:
echo $1
echo

curl --header "Authorization: token $TOKEN" \
        --header 'Accept: application/vnd.github.v3.raw' \
        --remote-name \
        --location $1

echo