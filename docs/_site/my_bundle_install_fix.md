[Issue Comment here](https://github.com/github/docs/issues/2177#issuecomment-1479957068)


>@hubwriter Back from 2023, for git-pages version 288, we are having dependency >problems with bundle install again, and here is my solution to all these dependency >error:
>
>sudo gem install colorator -v 1.1.0
>sudo gem install forwardable-extended -v 2.6.0
>sudo apt-get install ruby-dev
>sudo gem install racc -v 1.6.2
>sudo gem install commonmarker -v 0.23.8
>sudo gem install http_parser.rb -v 0.8.0
>sudo gem install jekyll-watch -v 2.2.1
>sudo gem install jekyll-sass-converter -v 1.5.2
>There might be more in your case~
>
>Basically, you need to install missing package with gem, and if required, install >ruby-dev as well
>
>If you have permission error on write to /var/lib/gems/ and /usr/local/bin, try
>
>sudo chown -R $(whoami) /var/lib/gems/
>sudo chown -R $(whoami) /usr/local/bin
>Good lunk!
