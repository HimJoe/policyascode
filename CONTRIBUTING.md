# Contributing to GRC Multi-Agent Governance System

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [Issues](https://github.com/HimJoe/policy-as-code/issues) section
2. If not, create a new issue with a clear title and description
3. Include steps to reproduce (for bugs) or detailed requirements (for features)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/HimJoe/policy-as-code.git
   cd policy-as-code
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Run the demo
   python demo.py

   # Test the web interface
   streamlit run streamlit_app.py

   # Run tests (if available)
   pytest tests/
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Provide a clear description of your changes

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

### Documentation
- Update README.md if adding new features
- Add examples for new functionality
- Keep documentation clear and concise

## Development Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install development dependencies**
   ```bash
   pip install pytest pytest-asyncio black flake8 mypy
   ```

3. **Run code formatting**
   ```bash
   black *.py
   flake8 *.py
   ```

## Areas for Contribution

### High Priority
- [ ] Add comprehensive test suite
- [ ] Implement persistent storage for audit logs
- [ ] Add authentication/authorization
- [ ] Create API endpoints (REST/GraphQL)
- [ ] Add Docker deployment configuration

### Medium Priority
- [ ] Support for additional file formats (Word, XML, JSON)
- [ ] Advanced analytics and reporting
- [ ] Machine learning for rule suggestions
- [ ] Natural language querying
- [ ] Integration examples (Flask, FastAPI, Django)

### Documentation
- [ ] Video tutorials
- [ ] More use case examples
- [ ] API documentation
- [ ] Deployment guides (AWS, Azure, GCP)

## Questions?

Feel free to:
- Open an issue for discussion
- Reach out to the maintainers
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
