venv_name=".venv"
requirements_file='requirements.txt'

# terminal colors
Red=$'\e[1;31m'
Yellow=$'\e[1;33m'
Normal=$'\e[1;0m'

# assumes the script is being executed from the workspace directory
cd src/
BASE_DIR=$PWD
echo $BASE_DIR

PROJECT_DIRS=(website xproductsapi xmessageprocessor)

for p_dir in "${PROJECT_DIRS[@]}" ; do 
  
  # check if dir exists
  if [[ -d "$p_dir" && ! -L "$p_dir" ]]; then
    echo "${Yellow}Working in $p_dir directory${Normal}" 
    cd $p_dir

    # check for existing virtual directory named $venv_name
    if [[ -d "$venv_name" ]]; then
        echo "Existing ${venv_name} directory found in ${p_dir}.\n${Red}Attempting to remove.${Normal}"
        rm -rf $venv_name
    else
        echo "${venv_name} directory not found in ${p_dir}."
    fi
    
    echo "${Yellow}Creating virtual environment in ${venv_name}${Normal}"
    python -m venv --prompt "${PWD##*/}-${venv_name:1}" ${venv_name}
    ${venv_name}/bin/pip install --upgrade pip wheel
    
    # install dependencies if requirements.txt exists
    if [[ -f "$requirements_file" ]]; then
        echo "${Yellow}A '$requirements_file' file was located."
        echo "${Yellow}Installing requirements.${Normal}"
        ${venv_name}/bin/pip install -r requirements.txt
    else
        echo "${Red}No '$requirements_file' file not found in ${PWD}.${Normal}"
    fi

    echo "Moving on... 🚙"
  fi; 
done