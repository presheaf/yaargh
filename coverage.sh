py.test --cov yaargh --cov-report term --cov-report html "$@" \
    && xdg-open htmlcov/index.html
