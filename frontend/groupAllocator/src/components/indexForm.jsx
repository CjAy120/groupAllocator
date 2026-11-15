import { useState } from 'react';

function IndexForm({ onRegister, disabled = false }) {
  const [name, setName] = useState('');
  const [indexNumber, setIndexNumber] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!name.trim() || !indexNumber.trim()) {
      setError('Please complete both fields.');
      return;
    }

    setError('');
    await onRegister({
      name: name.trim().replace(/\s+/g, ' '),
      indexNumber: indexNumber.trim().toUpperCase(),
    });
  };

  return (
    <section className="registration-section">
      <div className="section-heading">
        <span className="eyebrow">REGISTRATION</span>
        <h2>Join a group</h2>
        <p>Enter your details to receive your group assignment.</p>
      </div>

      <form className="registration-form" onSubmit={handleSubmit}>
        <div className="form-field">
          <label htmlFor="studentName">Full name</label>
          <input
            type="text"
            id="studentName"
            placeholder="Enter your full name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            autoComplete="name"
            required
            maxLength={150}
            disabled={disabled}
          />
        </div>

        <div className="form-field">
          <label htmlFor="indexNumber">Index number</label>
          <input
            type="text"
            id="indexNumber"
            placeholder="Enter your index number"
            value={indexNumber}
            onChange={(event) => setIndexNumber(event.target.value)}
            autoComplete="off"
            required
            maxLength={50}
            disabled={disabled}
          />
        </div>

        {error && <p className="form-error">{error}</p>}

        <button
          type="submit"
          className="primary-button"
          disabled={disabled}
        >
          {disabled ? 'Registering…' : 'Register and join group'}
        </button>
      </form>
    </section>
  );
}

export default IndexForm;
