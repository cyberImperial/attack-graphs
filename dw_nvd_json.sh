#!/bin/bash
 
# export https_proxy=<ADD HERE YOUR PROXY IF NEEDED>
 
START_YEAR=2002
END_YEAR=$(date +'%Y')
DOWNLOAD_DIR=.
 
CVE_MODIFIED_URL='https://static.nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-modified.json.gz'

CVE_BASE_URL='https://static.nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-%d.json.gz'
 
if [[ $# -eq 1 ]] ; then
    DOWNLOAD_DIR=$1
fi
 
START_TIME=$(date +%s)
 
download () {
    echo
    echo "Starting download of $1"
    OUTPUT_FILE=${1##*/}
    wget --no-check-certificate $1 -P $DOWNLOAD_DIR -O $OUTPUT_FILE
    if [ "$?" != 0 ]; then
        echo "ERROR: Downloading of $1 failed."
        exit 1
    fi
    
    echo "Extracting $OUTPUT_FILE" 
    gzip -df $OUTPUT_FILE
    
    if [ "$?" != 0 ]; then
        echo "ERROR: Extracting of $OUTPUT_FILE failed."
        exit 1
    fi
    
    echo "Download of $1 sucessfully completed."
    echo
}
 
echo "Starting download of NVD files ..."
download "$CVE_MODIFIED_URL"
 
for ((i=$START_YEAR;i<=$END_YEAR;i++));
do
    download "${CVE_BASE_URL//%d/$i}" 
    
done
 
END_TIME=$(date +%s)
DURATION=$((END_TIME-START_TIME))
echo "Download of NVD files successfully completed in $DURATION seconds."
