with (import <nixpkgs> {});
mkShell {
  name = "db final project shell";
  buildInputs = [ 
    (python3.withPackages (ps: with ps; [ 
      flask
      pg8000
      matplotlib
    ]))
  ];
}
