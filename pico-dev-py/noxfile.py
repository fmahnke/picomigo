import nox


@nox.session(reuse_venv=True)
def typing(session):
    session.run('basedpyright', external=True)
    # session.run('mypy', external=True)


@nox.session(reuse_venv=True)
def lint(session):
    session.run('flake8', 'src', 'tests', external=True)


@nox.session(reuse_venv=True)
def tests(session):
    session.run('coverage', 'run', '-m', 'pytest', external=True)
    session.run('coverage', 'combine', '--append', external=True)
    session.run(
        'coverage',
        'report',
        '--skip-empty',
        '--format',
        'total',
        external=True,
    )
