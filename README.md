# contactMgmtPy
contact management app pilot version

## Login options
User can choose one of the following login options [0-5]: \
[0] exit the program \
[1] login with username and password (account needed)\
[2] create login profile \
[3] change username and password (login required)\
[4] delete login profile (login required)\
[5] contact developer for any questions or feedback


### [0] exit the program
Program terminates.

### [1] login with username and password (account needed)
User must have an account before logging in. \
If user doesn't have an account, user can create one through `login option [2]`. \
User have five attempts to successfully login. \

After the fifth failed attempt, user is redirected to the `login options`. \
After a successful login, user is redirected to the `contacts list`.

### [2] create login profile
User can create an account with 'valid' username and password.
- 'valid' means that both username and password meet all the validation criteria:
  - username must be unique and less than 24 characters.
  - password must be between 8-12 characters.
  - password must have at least one special character: !@#$%^&*()-_+=
  - password must have at least one number.
  - password must have at least one uppercase.

### [3] change username and password (login required)
User can change username and password. \
User must first verify the correct username and password before the change. \
User must follow the same validation criteria listed in `login option [2]`.

### [4] delete login profile (login required)
User can delete their login profile. \
User must first verify the correct username and password before the deletion. \
**Once user deletes, all associated contacts will be erased permanently.**

### [5] contact developer for any questions or feedback
User can reach out to the developer via email for any questions or feedback.
