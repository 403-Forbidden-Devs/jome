import os
import sys

import api4jenkins
from api4jenkins import Jenkins
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


JENKINS_URL = "localhost:8080" if os.environ.get("URL") is None else os.environ.get("URL")
logging.log(logging.INFO, "Starting Jenkins")
USER = "admin" if os.environ.get("JENKINS_USER") is None else os.environ.get("JENKINS_USER")
PASSWORD = "password" if os.environ.get("PASSWORD") is None else os.environ.get("PASSWORD")
API_KEY = "password" if os.environ.get("API_KEY") is None else os.environ.get("API_KEY")
server = Jenkins('https://jenkins.piramalfinance.com', auth=(USER, PASSWORD))

version = server.version
logging.log(logging.INFO, "Jenkins version: {}".format(version))


def get_service_info(service_name):
    job = server.get_job(service_name)
    print(job)

def find_job(job_name):
    for entities in server:
        print("{}: {}".format(entities.name, entities.description))
        print("{}".format(type(entities)))
        if type(entities) is api4jenkins.job.Folder:
            for job in entities.iter():
                print("type of inside jobs: {}".format(type(job)))
                if type(job) is api4jenkins.job.FreeStyleProject and job_name in job.full_name:
                    print(job.get_last_completed_build())
                if type(job) is api4jenkins.job.Folder:
                    for job in entities.iter():
                        print("type of inside jobs level 2: {}".format(type(job)))
                        if type(job) is api4jenkins.job.FreeStyleProject and job_name in job.full_name:
                            print(job.get_last_completed_build())

def find_job_recursive(folder_list, entity, job_name):
    '''
    function to recursively look into the jenkins directory and find the job based on its name
    :param folder_list: list of jenkins folder, which contains folder which are recursively searched
    :param entity: jenkins entity
    :param job_name: jenkins job name for which we want to find the description
    :return: prints the jenkins job description
    '''
    if type(entity) is api4jenkins.job and entity.name == job_name:
        print(entity.get_last_completed_build())
    if entity in folder_list:
        folder_list = folder_list[:]





def iter_job():
    for job in server.iter():
        print(job)
        print(dir(job))
        print("full name : {}".format(job.full_name))
        print("full display name: {}".format(job.full_display_name))
        print("url: {}".format(job.url))
        if(type(job) is not api4jenkins.Folder):
            print("status: {}".format(job.status))
        if type(job) is api4jenkins.Folder:
            print(f"Getting in {job}\n")
            for job_1 in job.iter():
                print(job_1)
                print(dir(job_1))
                print("full name : {}".format(job_1.full_name))
                print("full display name: {}".format(job_1.full_display_name))
                print("url: {}".format(job.url))
                print("last build status: {}".format(job_1.get_last_completed_build()))
                print("dir of build: {}".format(dir(job_1.get_last_completed_build())))
                print("detail of the last job: {}".format(job_1.get_last_completed_build().get_parameters()))
                break
        break


if __name__ == '__main__':
    # service_name = sys.argv[1]
    name = sys.argv[1]
    # find_job(name)
    iter_job()
