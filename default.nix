with import <nixpkgs> {};
let
  gatt = with python3.pkgs; buildPythonPackage rec {
    pname = "gatt";
    version = "0.2.7";

    src = fetchPypi {
      inherit pname version;
      sha256 = "626d9de24a178b6eaff78c31b0bd29f962681da7caf18eb20363f6288d014e3a";
    };

    propagatedBuildInputs = [ dbus-python pygobject3 ];
  };
in stdenv.mkDerivation {
  name = "env";
  buildInputs = [
    bashInteractive
    gatt
  ];
}
