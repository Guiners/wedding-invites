CREATE TABLE projects (
    id BIGSERIAL PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    code VARCHAR(8) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    UNIQUE (code)
);

CREATE TABLE event_info (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL,

    brides_first_name VARCHAR(255) NOT NULL,
    brides_last_name VARCHAR(255) NOT NULL,
    brides_phone_number VARCHAR(255) NOT NULL,

    grooms_first_name VARCHAR(255) NOT NULL,
    grooms_last_name VARCHAR(255) NOT NULL,
    grooms_phone_number VARCHAR(255) NOT NULL,

    wedding_date DATE NOT NULL,
    wedding_time TIME NOT NULL,
    rsvp_deadline_date DATE NOT NULL,

    name_of_the_church VARCHAR(255) NOT NULL,
    church_address VARCHAR(255) NOT NULL,

    name_of_the_wedding_venue VARCHAR(255) NOT NULL,
    wedding_venue_address VARCHAR(255) NOT NULL,

    flowers_or_alcohol VARCHAR(255) NOT NULL,
    gifts_or_cash VARCHAR(255) NOT NULL,

    children_be_invited BOOLEAN NOT NULL DEFAULT TRUE,

    UNIQUE (project_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE invitation_info (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL,

    invitation_model VARCHAR(255),
    additional_card VARCHAR(255),

    envelope_color VARCHAR(255) NOT NULL,
    envelope_personalization BOOLEAN NOT NULL DEFAULT FALSE,
    envelope_wax_seal BOOLEAN NOT NULL DEFAULT FALSE,
    envelope_ribbon BOOLEAN NOT NULL DEFAULT FALSE,
    envelope_foil_stamping BOOLEAN NOT NULL DEFAULT FALSE,

    song_link VARCHAR(255),

    UNIQUE (project_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE guests (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL,

    invited_guests VARCHAR(255) NOT NULL,
    special_invitation VARCHAR(255),
    with_plus_one BOOLEAN NOT NULL DEFAULT FALSE,
    with_children BOOLEAN NOT NULL DEFAULT FALSE,
    with_accommodation BOOLEAN NOT NULL DEFAULT FALSE,
    code VARCHAR(8) NOT NULL,

    UNIQUE (code),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
