let
  pkgs = import <nixpkgs> {};
  python = pkgs.python312;
  pythonPackages = python.pkgs;
  libPath = with pkgs; lib.makeLibraryPath [];
in with pkgs; mkShell {
  packages = [
    pkgs.gnumake
    pkgs.black 
    pkgs.pandoc
    pkgs.tailwindcss_4
    pkgs.watchman

    pythonPackages.python-dotenv
    pythonPackages.flask
  ];

  buildInputs = [];

  shellHook = ''
    SOURCE_DATE_EPOCH=$(date +%s)
    export "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${libPath}"
    
    VENV=.venv

    if test ! -d $VENV; then
      python3.12 -m venv $VENV
    fi
    
    source ./$VENV/bin/activate
    export PYTHONPATH=`pwd`/$VENV/${python.sitePackages}/:$PYTHONPATH:.

    pip install --upgrade pip
    pip install -r requirements.txt
  '';

  postShellHook = ''
    ln -sf ${python.sitePackages}/* ./.venv/lib/python3.12/site-packages
  '';
}