pipeline {
  agent any
  stages {
    stage('Run tests') {
      steps {
        sh 'python3 -m virtualenv env'
        sh 'source env/bin/activate'
        sh 'python -m pip install -r requirements.txt'
        sh 'python -m pytest --cov=app --cov-report=term-missing'
      }
    }
  }
  environment {
    DB_NAME = 'fastfoodfast'
    DB_USER = 'postgres'
    DB_PASSWORD = 'Nyamwaro2012'
  }
}