CREATE TABLE "users" (
  "id" interger PRIMARY KEY,
  "full_name" varchar(100),
  "email" varchar(255),
  "hashed_password" varchar(255),
  "created_at" timestamp,
  "changed_at" timestamp
);

ALTER TABLE "application_files" ADD FOREIGN KEY ("application_id") REFERENCES "applications" ("id");


ALTER TABLE "applications" ADD FOREIGN KEY ("id") REFERENCES "application_history" ("application_id");

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "application_history" ("changed_by");

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "applications" ("changed_by");

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "applications" ("user_id");

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "organisations" ("super_admin_id");

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "user_organisations" ("changed_by");

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "grants" ("created_by");

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "grants" ("changed_by");

ALTER TABLE "user_organisations" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_organisations" ADD FOREIGN KEY ("organisation_id") REFERENCES "organisations" ("id");

CREATE TABLE "organisations" (
                                 "id" integer PRIMARY KEY,
                                 "name" varchar(100),
                                 "location" varchar(60),
                                 "description" varchar(255),
                                 "super_admin_id" integer,
                                 "created_at" datetime,
                                 "changed_at" datetime
);

CREATE TABLE "grants" (
                          "id" integer PRIMARY KEY,
                          "title" varchar(100),
                          "description" varchar(max),
  "requirements" varchar(max),
  "status" varchar(3),
  "app_start_date" datetime,
  "app_end_date" datetime,
  "created_at" datetime,
  "created_by" integer,
  "changed_at" datetime,
  "changed_by" integer
);

CREATE TABLE "user_organisations" (
                                      "user_id" integer,
                                      "organisation_id" integer,
                                      "is_adminstrator" bool,
                                      "created_at" datetime,
                                      "changed_at" datetime,
                                      "changed_by" integer
);

CREATE TABLE "applications" (
                                "id" integer PRIMARY KEY,
                                "title" varchar,
                                "body" text,
                                "user_id" integer,
                                "status" varchar(3),
                                "created_at" datetime,
                                "changed_by" integer,
                                "changed_at" datetime
);

CREATE TABLE "application_files" (
                                     "id" integer PRIMARY KEY,
                                     "application_id" integer,
                                     "description" varchar(100),
                                     "file_storage_key" varchar(100),
                                     "is_archived" bool,
                                     "created_at" datetime,
                                     "archived_at" datetime
);

CREATE TABLE "application_history" (
                                       "id" integer PRIMARY KEY,
                                       "application_id" integer,
                                       "old_status" varchar(3),
                                       "new_status" varchar(3),
                                       "remarks" varchar(255),
                                       "changed_at" datetime,
                                       "changed_by" interger
);
