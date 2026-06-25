  import sys
  import xml.etree.ElementTree as ET

  ns = {"wadl": "http://wadl.dev.java.net/2009/02"}

  tree = ET.parse(sys.argv[1])
  root = tree.getroot()

  def text(el):
      if el is None:
          return ""
      return " ".join("".join(el.itertext()).split())

  def walk_resource(res, prefix=""):
      path = res.attrib.get("path", "")
      full_path = "/".join(x.strip("/") for x in [prefix, path] if x)
      full_path = "/" + full_path if full_path else "/"

      for method in res.findall("wadl:method", ns):
          method_name = method.attrib.get("name", "")
          method_id = method.attrib.get("id", "")
          doc = text(method.find("wadl:doc", ns))

          params = []
          req = method.find("wadl:request", ns)
          if req is not None:
              for p in req.findall(".//wadl:param", ns):
                  params.append(
                      f"{p.attrib.get('style','')}:{p.attrib.get('name','')}:{p.attrib.get('type','')}"
                  )

          print(f"{method_name}\t{full_path}\t{method_id}\t{doc}\t{', '.join(params)}")

      for child in res.findall("wadl:resource", ns):
          walk_resource(child, full_path)

  for resources in root.findall("wadl:resources", ns):
      base = resources.attrib.get("base", "")
      print(f"# BASE: {base}")
      for res in resources.findall("wadl:resource", ns):
          walk_resource(res)
