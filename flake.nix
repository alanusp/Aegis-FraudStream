{
  description = "Aegis FraudStream dev shell";
  inputs = { nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05"; };
  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in {
      devShells.x86_64-linux.default = pkgs.mkShell {
        packages = with pkgs; [ python311 python311Packages.pip uv ruff mypy nodejs_22 docker-compose k6 ];
        shellHook = ''
          echo "Dev shell ready. Use: uv pip install -e '.[dev]' --system"
        '';
      };
    };
}
