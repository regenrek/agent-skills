# Python Formula Template

Use when the project ships a Python CLI.

```ruby
class Yourtool < Formula
  include Language::Python::Virtualenv

  desc "Short description"
  homepage "https://github.com/OWNER/yourtool"
  url "https://github.com/OWNER/yourtool/archive/refs/tags/v1.2.3.tar.gz"
  sha256 "PUT_SHA256_HERE"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/yourtool", "--version"
  end
end
```

Notes:
- Add `resource` blocks for all Python dependencies if they are not vendored.
- Use the Python version that matches the project requirements.
