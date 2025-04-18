with (import <nixpkgs> {});
mkShell {
  name = "db final project shell";
  buildInputs = [ 
    (python3.withPackages (ps: with ps; [ 
      requests
      flask
      pg8000
    ]))
  ];
}
