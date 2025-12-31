# Go Formula Template

Use when the project builds with Go.

```ruby
class Yourtool < Formula
  desc "Short description"
  homepage "https://github.com/OWNER/yourtool"
  url "https://github.com/OWNER/yourtool/archive/refs/tags/v1.2.3.tar.gz"
  sha256 "PUT_SHA256_HERE"
  license "MIT"

  depends_on "go" => :build

  def install
    system "go", "build", *std_go_args(ldflags: "-s -w"), "./cmd/yourtool"
  end

  test do
    system "#{bin}/yourtool", "--version"
  end
end
```

Notes:
- Replace the build path with the correct main package if it is not under `./cmd/<name>`.
- Add any required build-time dependencies.
