import os

from invoke import task

# Run from project root directory
scriptdir = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptdir)


@task
def format(ctx):
    """Run black and isort"""
    for cmd in ("black .", "isort ."):
        ctx.run(cmd, echo=True)


@task
def check(ctx):
    """Run flake8"""
    for cmd in ("flake8 .",):
        ctx.run(cmd, echo=True)


@task
def test(ctx):
    """Run tests"""
    for cmd in ("pytest --cov --junitxml=build/reports/tests.xml",):
        ctx.run(cmd, echo=True)


@task
def build(ctx):
    """Build"""
    for cmd in ("poetry build",):
        ctx.run(cmd, echo=True)


@task
def generate_doc(ctx):
    """Generate documentation"""
    for cmd in ("sphinx-apidoc -P -f -o docs/_source src/my_project",):
        ctx.run(cmd, echo=True)


@task(generate_doc)
def build_doc(ctx):
    """Build documentation"""
    for cmd in ("sphinx-build -b html docs dist/docs",):
        ctx.run(cmd, echo=True)


@task
def build_exe(ctx):
    """Build documentation"""
    for cmd in ("pyinstaller setup/my_project.spec --noconfirm",):
        ctx.run(cmd, echo=True)


@task
def build_blender(ctx):
    """Build blender add-on"""
    source = "blender_linesplan"
    target = "../build/blender-linesplan.zip"
    with ctx.cd("src"):
        for cmd in (
            "mkdir -p ../build/",
            f"rm -f {target}",
            f"rm -rf {source}/__pycache__",
            f"zip -r {target} {source}",
        ):
            ctx.run(cmd, echo=True)
