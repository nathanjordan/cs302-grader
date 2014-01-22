import database
import os
import zipfile
import shutil
import glob
import subprocess
import xml.etree.ElementTree as ElementTree

current_path = os.path.dirname(os.path.abspath(__file__))


def unzip_assignment_archive(submission_id):
    # get the submission object
    submission = database.db_session.query(
        database.Submission).get(submission_id)
    # generate the path to the submission directory
    sub_dir = os.path.join(current_path,
                           '..',
                           'submissions',
                           'assignment' + str(submission.assignment_id),
                           submission.net_id,
                           str(submission.id)
                           )
    # path to the students submission archive
    archive_path = sub_dir + '/' + submission.filename
    # register and extract the archive
    archive = zipfile.ZipFile(archive_path)
    archive.extractall(sub_dir)
    # remove the .zip extension from the file
    #extracted_folder = os.path.splitext(archive_path)[0]
    # get a list of files in the extracted folder
    #student_files = glob.glob(extracted_folder + '/*')
    # move each of these files to the submission directory
    #for f in student_files:
    #    shutil.move(f, sub_dir)
    # delete the extracted folder
    #shutil.rmtree(extracted_folder)


def copy_assignment_files(submission_id):
    # get the submission object
    submission = database.db_session.query(
        database.Submission).get(submission_id)
    # generate the path to the submission directory
    sub_dir = os.path.join(current_path,
                           '..',
                           'submissions',
                           'assignment' + str(submission.assignment_id),
                           submission.net_id,
                           str(submission.id)
                           )
    # generate the path to the directory containing assignment files
    assignment_dir = os.path.join(current_path,
                                  '..',
                                  'assignments',
                                  'assignment' + str(submission.assignment_id)
                                  )
    # create a list of the files in the assignment directory
    files = glob.glob(assignment_dir + '/*')
    # copy these files into the submission directory
    for filename in files:
        shutil.copy(filename, sub_dir)


def build_submission(submission_id):
    # get the submission object
    submission = database.db_session.query(
        database.Submission).get(submission_id)
    # generate the path to the submission directory
    sub_dir = os.path.join(current_path,
                           '..',
                           'submissions',
                           'assignment' + str(submission.assignment_id),
                           submission.net_id,
                           str(submission.id)
                           )
    sub_dir = os.path.realpath(sub_dir)
    # call make in the submission directory
    try:
        subprocess.check_call('make -C ' + sub_dir, shell=True)
    # if theres an error building do something
    except subprocess.CalledProcessError as e:
        return False
    return True


def grade_unit_test(test_id, submission_id):
    # get the submission object
    submission = database.db_session.query(
        database.Submission).get(submission_id)
    # get test
    test = database.db_session.query(
        database.Test).get(test_id)
    # create a testsubmission
    submit_test = database.SubmissionTest(test=test, submission=submission)
    # get the submission directory
    sub_dir = os.path.join(current_path,
                           '..',
                           'submissions',
                           'assignment' + str(submission.assignment_id),
                           submission.net_id,
                           str(submission.id)
                           )
    sub_dir = os.path.realpath(sub_dir)
    # generate the path to the executable
    exec_file = sub_dir + '/' + test.executable_filename
    # run the test executable
    proc = subprocess.Popen([exec_file, '-r', 'xml'], stdout=subprocess.PIPE)
    # get the xml output from the test executable
    out, err = proc.communicate()
    # get the root XML element
    root = ElementTree.fromstring(out)
    # Get the results node
    results = root.find('OverallResults')
    # count successes and failures
    successes = int(results.get('successes'))
    failures = int(results.get('failures'))
    # calculate the percentage and score
    percent = successes / float(successes + failures)
    score = round(percent * test.points)
    submit_test.score = score
    print score

def grade_diff_test(test_id, submission_id):
    return
