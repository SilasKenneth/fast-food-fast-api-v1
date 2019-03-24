pipeline {
  agent any
  stages {
    stage('Run tests') {
      steps {
        echo 'Hello world'
        sh '''python3 -m pip install -r requirements.txt
python3 -m pytest --cov=app --cov-report=term-missing'''
      }
    }
  }
  environment {
    DB_NAME = 'fastfoodfast'
    DB_USER = 'postgres'
    DB_PASSWORD = 'Nyamwaro2012'
  }
}