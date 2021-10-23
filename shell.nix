with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "cpp-env";
  nativeBuildInputs = [
    gcc10
    curl
    cmake
    ccache
    rsync
    unzip

    # Example Build-time Additional Dependencies
    pkgconfig
  ];
  buildInputs = [
    # Example Run-time Additional Dependencies
    clang-tools
  ];
  hardeningDisable = [ "format" "fortify" ];
}
