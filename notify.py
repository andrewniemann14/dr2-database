
def notify(challenges):
  for c in challenges:
    print(c["vehicle_class"] + " in " + c["country"])

# add some way to prettify the output
# e.g. eRallyGrpB4wdCaps => Grp B 4WD
# dictionary would probably be simplest

def prettify(raw):

  pretty = {
    "eRallyGrpB4wdCaps": "Grp B 4WD",
  }


  return pretty[raw]


print(prettify("eRallyGrpB4wdCaps"))