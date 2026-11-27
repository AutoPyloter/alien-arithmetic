import OPNCheck
def main (args : List String) : IO Unit := do
  let k := (args.headD "6").toNat!
  IO.println s!"K={k} run={run 2000 (init k)}"
