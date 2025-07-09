
# https://github.com/itsmaxymoo/create-license
# refer this repo to create the license command

from handlers.license import licence_helper
from handlers import pyprompt

from datetime import datetime

pyp = pyprompt.Terminal()

def gen(licence_name,project_name,ask=False):

    year = datetime.now().year
    final_licence_name = None
    final_project_name = None

    if ask:



        resp_licence_name = pyp.mcq(question='Please select a license for your project', options=licence_helper.list_licenses())
        pyp.good(f"Selected license: {resp_licence_name}")
        resp_project_name = pyp.ask("Please enter your project name")

        final_project_name = resp_project_name
        final_licence_name = resp_licence_name
    else:

        final_licence_name = licence_name.upper()
        final_project_name = project_name.upper()



    licenseTXT = licence_helper.get_license(name=final_licence_name,year=year,author=final_project_name)

    with open("LICENSE", "w") as f:
      f.write(licenseTXT)
    pyp.good("LICENSE file created successfully.")


def list_licence():
    pyp.show_list(title="Licence List",items=licence_helper.list_licenses())



def show(licence_name,ask=False):
    year = datetime.now().year
    final_licence_name = None

    if ask:

        resp_licence_name = pyp.mcq(question='Please select a license for your project', options=licence_helper.list_licenses())
        pyp.good(f"Selected license: {resp_licence_name}")

        final_licence_name = resp_licence_name
    else:

        final_licence_name = licence_name.upper()



    licenseTXT = licence_helper.get_license(name=final_licence_name,year=year,author='PROJECT NAME')

    pyp.markdown(licenseTXT)
