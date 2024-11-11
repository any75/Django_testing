import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Course
@pytest.fixture
def apiclient():
    return APIClient
@pytest.fixture
def coursefactory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory
@pytest.fixture
def studentfactory():
    def factory(**kwargs):
        return baker.make('students.Student', **kwargs)
    return factory
@pytest.mark.django_db
def test_api_course(apiclient, coursefactory):
    course = coursefactory(name = 'testcourse')
    url = f'/api/v1/courses/{course.id}'
    response = apiclient.get(url)
    assert response.status_code == 200
    assert response.data['name'] == 'testcourse'
@pytest.mark.django_db
def test_list_courses(apiclient, coursefactory):
    coursefactory(name = '1')
    coursefactory(name = '2')
    url = '/api/v1/courses/'
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
@pytest.mark.django_db
def test_filter_id(apiclient, coursefactory):
    course1 = coursefactory(name = 'course 1', id = 1)
    course2 = coursefactory(name = 'course 2', id = 2)
    url = '/api/v1/courses/'
    response = apiclient.get(url, data = {'id': course1.id})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0] ['id'] == course1.id
@pytest.mark.django_db
def test_filter_name(apiclient, coursefactory):
    course1 = coursefactory(name = 'course 1', id = 1)
    course2 = coursefactory(name = 'course 2', id = 2)
    url = '/api/v1/courses/'
    response = apiclient.get(url, data = {'name': course2.name})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0] ['name'] == course1.name
@pytest.mark.django_db
def test_new_course(apiclient):
    data = {'name': 'new course'}
    url = '/api/v1/courses/'
    response = apiclient.post(url, data = data, format = 'json')
    assert response.status_code == 201
    assert response.data ['name'] == 'new course'
@pytest.mark.django_db
def test_update_course(apiclient, coursefactory):
    course = coursefactory(name = 'course1')
    data = {'name': 'update course1'}
    url = f'/api/v1/courses/{course.id}'
    response = apiclient.patch(url, data = data, format = 'json')
    assert response.status_code == 200
    assert response.data ['name'] == 'update course'
@pytest.mark.django_db
def test_delete_course(apiclient, coursefactory):
    course = coursefactory()
    url = f'/api/v1/courses/{course.id}'
    response = apiclient.delete(url)
    aasert response.status_code == 204
    

