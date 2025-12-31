# Node/TypeScript Formula Template

Use when the project ships a Node-based CLI (JavaScript or TypeScript).

```ruby
class Yourtool < Formula
  desc "Short description"
  homepage "https://github.com/OWNER/yourtool"
  url "https://github.com/OWNER/yourtool/archive/refs/tags/v1.2.3.tar.gz"
  sha256 "PUT_SHA256_HERE"
  license "MIT"

  depends_on "node"

  def install
    system "npm", "install", *std_npm_args
  end

  test do
    system "#{bin}/yourtool", "--version"
  end
end
```

Notes:
- If a build step is required, run `npm run build` before `npm install`.
- Ensure the package exposes a `bin` entry so the CLI is linked into `bin/`.
