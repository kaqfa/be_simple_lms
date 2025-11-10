# 🤝 Contributing to Be Simple LMS

Thank you for your interest in contributing to Be Simple LMS! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Documentation](#documentation)

---

## 📜 Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and follow our Code of Conduct:

- Be respectful and inclusive
- Provide constructive feedback
- Report inappropriate behavior
- Respect diverse perspectives and backgrounds

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 16
- Redis
- Docker & Docker Compose (recommended)
- Git

### Fork & Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/be_simple_lms.git
   cd be_simple_lms
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/original-repo/be_simple_lms.git
   ```

---

## 💻 Development Setup

### Using Docker (Recommended)

```bash
# Build and start services
docker-compose up -d

# Run migrations
docker-compose exec web python code/manage.py migrate

# Create superuser
docker-compose exec web python code/manage.py createsuperuser

# Load sample data (optional)
docker-compose exec web python code/importer2.py
```

Access the app at `http://localhost:8001/api/v1/`

### Local Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Run migrations
python code/manage.py migrate

# Create superuser
python code/manage.py createsuperuser

# Start development server
python code/manage.py runserver
```

---

## 🔄 Making Changes

### Branch Naming Convention

Create a new branch for your work:

```bash
# Feature branch
git checkout -b feature/your-feature-name

# Bugfix branch
git checkout -b fix/bug-description

# Documentation branch
git checkout -b docs/documentation-update

# Task from roadmap
git checkout -b task/task-number-short-description
```

### Branch from Latest

Always ensure you're working from the latest code:

```bash
git fetch upstream
git rebase upstream/main
```

### Making Your Changes

1. Create a new branch (as above)
2. Make your changes
3. Test locally
4. Commit with clear messages (see [Commit Guidelines](#commit-guidelines))
5. Push to your fork:
   ```bash
   git push origin your-branch-name
   ```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run with coverage
pytest --cov=lms_core --cov-report=html

# Run specific test
pytest tests/test_models.py::TestCourseModel::test_course_creation
```

### Writing Tests

Tests should be placed in the `tests/` directory, mirroring the app structure:

```
tests/
├── test_models.py
├── test_api.py
├── test_views.py
└── test_services.py
```

Example test structure:

```python
import pytest
from django.contrib.auth.models import User
from lms_core.models import Course

@pytest.fixture
def sample_user():
    """Create a sample user for testing"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.mark.django_db
class TestCourseModel:

    def test_course_creation(self, sample_user):
        """Test creating a new course"""
        course = Course.objects.create(
            title="Python Basics",
            description="Learn Python",
            teacher=sample_user,
            price=99.99
        )
        assert course.title == "Python Basics"
        assert course.teacher == sample_user
```

### Test Coverage Requirements

- **Minimum 80% code coverage** for new code
- All API endpoints must have integration tests
- All models must have unit tests
- All services/utilities must have tests

---

## 💬 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc)
- `refactor`: Code refactoring without feature changes
- `test`: Adding or updating tests
- `chore`: Build, dependency updates, etc

### Scope

The scope specifies what part of the codebase is affected:
- `quiz`: Quiz/Assessment system
- `notifications`: Notification system
- `progress`: Progress tracking
- `assignments`: Assignment system
- `api`: API endpoints
- `models`: Database models
- `tests`: Testing
- `docs`: Documentation

### Subject

- Use imperative mood ("add feature" not "added feature")
- Don't capitalize first letter
- No period (.) at the end
- Maximum 50 characters

### Body

- Explain what and why, not how
- Wrap at 72 characters
- Separate from subject with blank line
- Use bullet points for multiple changes

### Footer

Reference related issues:

```
Closes #123
Related to #456
```

### Examples

```
feat(quiz): add automatic scoring for multiple choice questions

Add auto-scoring algorithm for multiple choice questions.
Implement QuestionOption model and update QuestionScore logic.

Closes #42
```

```
fix(api): prevent N+1 queries in course list endpoint

Use select_related() for teacher and prefetch_related() for
members to reduce database queries from 50+ to 2.

Fixes #98
```

---

## 🔀 Pull Request Process

### Before Creating PR

1. **Update from upstream:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests locally:**
   ```bash
   pytest
   pytest --cov=lms_core
   ```

3. **Check code style:**
   ```bash
   black code/
   flake8 code/
   ```

4. **Update documentation** if needed

### Creating PR

1. Push your branch to your fork
2. Go to GitHub and create a Pull Request
3. Fill in the PR template:

```markdown
## Description
Brief description of your changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Breaking change

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing
- [ ] Test coverage >= 80%

## Related Issues
Closes #(issue number)

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Database migrations created (if needed)
- [ ] No breaking changes
- [ ] Reviewed own code for obvious errors
```

### Review Process

1. At least 1 maintainer review required
2. All tests must pass
3. Coverage must be >= 80%
4. Code style must be consistent
5. Address feedback and re-request review

---

## 🎨 Code Style

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some additions:

#### Tools

```bash
# Format code with Black
black code/

# Check style with Flake8
flake8 code/

# Check imports
isort code/

# Type checking (optional)
mypy code/
```

#### Guidelines

- Line length: 88 characters (Black default)
- Indentation: 4 spaces
- Use type hints for function parameters and returns
- Use docstrings for modules, classes, and functions

### Example

```python
from typing import Optional
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    """Model representing an online course.

    Attributes:
        title: Course title
        description: Course description
        teacher: Instructor for the course
        price: Course price in USD
    """

    title: str = models.CharField(max_length=200)
    description: str = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    price: float = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        """Return string representation of course"""
        return self.title

    def is_free(self) -> bool:
        """Check if course is free"""
        return self.price == 0
```

### Django Conventions

- Model names: Singular and PascalCase (Course, not Courses)
- Model methods: lowercase_with_underscores
- Always use `on_delete=models.CASCADE` or appropriate option
- Use `verbose_name` and `verbose_name_plural` in Meta
- Use `related_name` for reverse relationships

---

## 📚 Documentation

### Code Comments

- Write comments for complex logic
- Explain WHY, not WHAT
- Keep comments up-to-date with code

```python
# Good
# Skip processing if user is inactive to improve performance
if not user.is_active:
    return None

# Avoid
# Set x to 1
x = 1
```

### Docstrings

Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings):

```python
def create_certificate(student_id: int, course_id: int) -> Certificate:
    """Generate certificate for course completion.

    Creates a PDF certificate for a student who has completed
    a course. The certificate is stored in the media folder.

    Args:
        student_id: ID of the student
        course_id: ID of the completed course

    Returns:
        Certificate object with PDF URL

    Raises:
        Student.DoesNotExist: If student not found
        Course.DoesNotExist: If course not found
        ValueError: If student hasn't completed the course
    """
```

### API Documentation

All API endpoints should be documented:

```python
@router.get("/courses/", tags=["courses"])
def list_courses(
    request: HttpRequest,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> List[CourseSchema]:
    """List all available courses.

    Query Parameters:
        skip: Number of courses to skip (default: 0)
        limit: Maximum courses to return (default: 20, max: 100)

    Returns:
        List of course objects

    Example:
        GET /api/v1/courses/?skip=0&limit=20
    """
```

### README Updates

- Update README for new features
- Include setup instructions if needed
- Update API endpoint documentation

---

## 🐛 Reporting Issues

### Bug Reports

Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs
- Your environment (Python version, OS, etc)

### Feature Requests

Include:
- Use case/motivation
- Proposed solution
- Alternatives considered
- Implementation complexity

---

## ❓ Questions?

- Check [README.md](README.md) first
- Check [ROADMAP.md](ROADMAP.md) for planned features
- Check [TODO.md](TODO.md) for task details
- Open an issue with label `question`
- Contact maintainers on GitHub Discussions

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to Be Simple LMS! 🎉**

