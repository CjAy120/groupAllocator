import { useState } from 'react';

function Groups({ onLookup, lookupResult, onClose, isLookingUp = false }) {
  const [indexNumber, setIndexNumber] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    const value = indexNumber.trim().toUpperCase();

    if (!value) {
      setError('Please enter your index number.');
      return;
    }

    setError('');
    onLookup(value);
  };

  return (
    <section className="lookup-section">
      <div className="section-heading">
        <span className="eyebrow">GROUP INFORMATION</span>
        <h2>Find your group</h2>
        <p>Already registered? Enter your index number to view your group.</p>
      </div>

      <form className="lookup-form" onSubmit={handleSubmit}>
        <div className="form-field">
          <label htmlFor="lookupIndex">Index number</label>
          <input
            type="text"
            id="lookupIndex"
            placeholder="Enter your index number"
            value={indexNumber}
            onChange={(event) => {
              setIndexNumber(event.target.value);
              setError('');
            }}
            autoComplete="off"
            maxLength={50}
            disabled={isLookingUp}
          />
        </div>

        {error && <p className="form-error">{error}</p>}

        <button type="submit" className="secondary-button" disabled={isLookingUp}>
          {isLookingUp ? 'Searching…' : 'Search allocation'}
        </button>
      </form>

      {lookupResult && (
        <div className="modal-overlay" onClick={onClose}>
          <div
            className="result-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="resultTitle"
            onClick={(event) => event.stopPropagation()}
          >
            <button
              type="button"
              className="modal-close"
              onClick={onClose}
              aria-label="Close"
            >
              ×
            </button>

            {lookupResult.status === 'not-found' ? (
              <div className="modal-content">
                <div className="result-indicator warning">!</div>
                <span className="eyebrow">ALLOCATION STATUS</span>
                <h3 id="resultTitle">No group assigned yet</h3>
                <p>
                  We couldn't find an allocation for this index number.
                  You may not have registered yet.
                </p>
                <button type="button" className="primary-button" onClick={onClose}>
                  Close
                </button>
              </div>
            ) : lookupResult.status === 'error' ? (
              <div className="modal-content">
                <div className="result-indicator warning">!</div>
                <span className="eyebrow">SEARCH ERROR</span>
                <h3 id="resultTitle">Couldn't complete the search</h3>
                <p>{lookupResult.message}</p>
                <button type="button" className="primary-button" onClick={onClose}>
                  Close
                </button>
              </div>
            ) : lookupResult.status === 'success' ? (
              <div className="modal-content">
                <div className="result-indicator success">✓</div>
                <span className="eyebrow">ALLOCATION FOUND</span>
                <h3 id="resultTitle">Your group</h3>

                <div className="assigned-group">
                  <span>GROUP</span>
                  <strong>{lookupResult.group.id}</strong>
                </div>

                <div className="member-heading">
                  <span>Group members</span>
                  <span>
                    {lookupResult.group.members.length}/{lookupResult.group.capacity}
                  </span>
                </div>

                <div className="member-list">
                  {lookupResult.group.members.map((member) => (
                    <div className="member-row" key={member.indexNumber}>
                      <div className="member-avatar">
                        {member.name.charAt(0).toUpperCase()}
                      </div>
                      <div className="member-details">
                        <strong>{member.name}</strong>
                        <span>{member.indexNumber}</span>
                      </div>
                      {member.indexNumber === lookupResult.student.indexNumber && (
                        <span className="you-label">You</span>
                      )}
                    </div>
                  ))}
                </div>

                <button
                  type="button"
                  className="secondary-button modal-button"
                  onClick={onClose}
                >
                  Done
                </button>
              </div>
            ) : null}
          </div>
        </div>
      )}
    </section>
  );
}

export default Groups;
