# Prebuilt Binary Formula Template

Use when the project provides prebuilt archives for each platform/arch.

```ruby
class Yourtool < Formula
  desc "Short description"
  homepage "https://github.com/OWNER/yourtool"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/OWNER/yourtool/releases/download/v1.2.3/yourtool_darwin_arm64.tar.gz"
      sha256 "PUT_SHA256_HERE"
    else
      url "https://github.com/OWNER/yourtool/releases/download/v1.2.3/yourtool_darwin_amd64.tar.gz"
      sha256 "PUT_SHA256_HERE"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/OWNER/yourtool/releases/download/v1.2.3/yourtool_linux_arm64.tar.gz"
      sha256 "PUT_SHA256_HERE"
    else
      url "https://github.com/OWNER/yourtool/releases/download/v1.2.3/yourtool_linux_amd64.tar.gz"
      sha256 "PUT_SHA256_HERE"
    end
  end

  def install
    bin.install "yourtool"
  end

  test do
    system "#{bin}/yourtool", "--version"
  end
end
```

Notes:
- Ensure the archive contains a single binary named `yourtool`.
- Add `version` if the URL does not encode it clearly.
