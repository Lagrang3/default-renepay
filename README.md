# Default Renepay

This plugin sets the payment rpc `renepay` as the default payment processor.
That is, every payment request addressed to the command `pay` will be redirected
to `renepay`.

## Installation

For general plugin installation instructions see the repos main
[README.md](https://github.com/lightningd/plugins/blob/master/README.md#Installation)

## FAQ

Q. How is this useful?

A. This is useful for people using their node through a remote control app
like Zeus that does not support `renepay`.

Q. Is it dangerous?

A. No. But if you get strange errors you can just disable the plugin and you
will be using `pay` again as default. And please make a bug report to the
developer of `renepay`.

Q. Will this improve the payment experience?

A. `renepay` is way younger than the standard `pay` plugin therefore it is not
very stable. But in theory it should produce the best payment reliability
possible given the information available to your node (as Rene Pickhardt puts
it: *optimally reliable payments*).
