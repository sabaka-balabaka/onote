# onote

Not so long ago, I have started this project. Maybe, you know such service, as privnote.com. It's a privacy web application, that stores one-time simple text notes, generates a link to note. Than it shows a noteto recepient, and it is removed from service. So easy, and so simple. But are privnotes are really secure? I don't know. There were cases, when url's were intercepted, and notes were intercepted also. I'm very eUxperienced in information privacy and security, and I know, that if I will send suck a note, I will have no warranty of privacy at all. But I want to send any data to any devices, no matter what technical architecture, and what laws are enforced there. That's why I decided to create my own privacy service. I think that suck a service must

- Work over TOR by default
- Use encrypted storage
- Do not allow direct peer-2-peer or client-2-server connections. IP Leak must be impossible
- Do not write logs
- Give an opportunity to control data, that is stored on an intermedia server
- Securely erase data on server-side
- Have a strong multi-factor authentication model
- Have an additional redirection layer for anonymous messages
- Have a private notification services, based on tor. It will be the base for future development of a messeger.
- Be easy in deployment on any cloud, any VM or even a mobile (Android (root)+Termux+Orbot).
- UI must be easy to learn and use. It must be minimalistic.
- Service must be mobile-friendly. For using base functionality, the only dependency, that must be satisfied, is TOR Browser.
- Service must have a self-destruction mechanism
- It must be based on open standards, and be open source.

I have deleloped a core prototype, that sends notes. It uses cleartext passwd file as an user db backend, and stores messages in inndividual files in a spool directory. Than I have opened an onion service, and transmitted an important information to my friends. Im my country, censorship exists, but it is not strict, and government have no tools agains TOR. But it is not so on all this planet. I always do web searh from different network locations simultaneously, and I see a difference. Nullifying artificial created barriers to communicate and get true and actual knowledge.

