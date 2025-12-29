# Rust Formula Template

Use when the project builds with Cargo.

```ruby
class Yourtool < Formula
  desc "Short description"
  homepage "https://github.com/OWNER/yourtool"
  url "https://github.com/OWNER/yourtool/archive/refs/tags/v1.2.3.tar.gz"
  sha256 "PUT_SHA256_HERE"
  license "MIT"

  depends_on "rust" => :build

  def install
    system "cargo", "install", *std_cargo_args
  end

  test do
    system "#{bin}/yourtool", "--version"
  end
end
```

Notes:
- If the binary name differs from the crate name, pass `--bin <name>`.
- For workspaces, use `--path <subdir>` or adjust the build command.
