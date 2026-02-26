const PASSWORD_TOGGLE_CLASSES = {
  wrapper: 'js-password-toggle__wrapper',
  input: 'js-password-toggle__input',
  button: 'js-password-toggle__button',
  passwordToggleIcon: 'js-password-toggle__password-toggle-icon',
  // passwordVisible: 'js-password-toggle__password-toggle-visible',
  // passwordHidden: 'js-password-toggle__password-toggle-hidden',
  passwordHidden: 'js-password-toggle__password-toggle-visible',
  passwordVisible: 'js-password-toggle__password-toggle-hidden',
};

const SVG_PATHS = {
  passwordVisible: 'M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z',
  passwordHidden: 'M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z'
};

function createWrapper(input, originalDisplay) {
  const wrapper = document.createElement('div');
  wrapper.className = PASSWORD_TOGGLE_CLASSES.wrapper;
  wrapper.style.display = originalDisplay;
  wrapper.style.width = window.getComputedStyle(input).width;
  wrapper.style.height = window.getComputedStyle(input).height;
  return wrapper;
}

function createToggleButton() {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = PASSWORD_TOGGLE_CLASSES.button;
  button.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" class="${PASSWORD_TOGGLE_CLASSES.passwordToggleIcon}">
      <path class="${PASSWORD_TOGGLE_CLASSES.passwordVisible}" d="${SVG_PATHS.passwordVisible}"/>
      <path class="${PASSWORD_TOGGLE_CLASSES.passwordHidden}" d="${SVG_PATHS.passwordHidden}"/>
    </svg>
  `;
  return button;
}

function togglePasswordVisibility(input, passwordVisibleIcon, passwordHiddenIcon) {
  if (input.type === 'password') {
    input.type = 'text';
    passwordVisibleIcon.style.display = 'none';
    passwordHiddenIcon.style.display = 'block';
  } else {
    input.type = 'password';
    passwordVisibleIcon.style.display = 'block';
    passwordHiddenIcon.style.display = 'none';
  }
}

function setupPasswordToggle(input) {
  const originalDisplay = window.getComputedStyle(input).display;
  input.classList.add(PASSWORD_TOGGLE_CLASSES.input);

  const wrapper = createWrapper(input, originalDisplay);
  input.parentNode.insertBefore(wrapper, input);
  input.style.paddingRight = '40px';
  input.style.width = wrapper.style.width;
  wrapper.appendChild(input);

  const toggleButton = createToggleButton();
  wrapper.appendChild(toggleButton);

  const passwordVisibleIcon = toggleButton.querySelector(`.${PASSWORD_TOGGLE_CLASSES.passwordVisible}`);
  const passwordHiddenIcon = toggleButton.querySelector(`.${PASSWORD_TOGGLE_CLASSES.passwordHidden}`);
  passwordVisibleIcon.style.display = 'none';

  toggleButton.addEventListener('click', () => togglePasswordVisibility(input, passwordVisibleIcon, passwordHiddenIcon));
}

function addStyles() {
  const style = document.createElement('style');
  style.textContent = `
    .${PASSWORD_TOGGLE_CLASSES.wrapper} {
      position: relative;
    }
    .${PASSWORD_TOGGLE_CLASSES.input} {
      box-sizing: border-box;
    }
    .${PASSWORD_TOGGLE_CLASSES.button} {
      position: absolute;
      top: 50%;
      right: 10px;
      transform: translateY(-50%);
      background: none;
      border: none;
      cursor: pointer;
      padding: 0;
      line-height: 0;
    }
    .${PASSWORD_TOGGLE_CLASSES.passwordToggleIcon} {
      width: 20px;
      height: 20px;
    }
  `;
  document.head.appendChild(style);
}

document.addEventListener('DOMContentLoaded', () => {
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  passwordInputs.forEach(setupPasswordToggle);
  addStyles();
});