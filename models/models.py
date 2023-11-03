from sqlalchemy import Column, DECIMAL, Date, Enum, ForeignKey, Index, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Address(Base):
    __tablename__ = 'Address'
    __table_args__ = (
        Index('UC_VillageGewogDzongkhag', 'villagename', 'gewog', 'dzongkhag', unique=True),
    )

    addressid = Column(Integer, primary_key=True)
    villagename = Column(String(255), nullable=False)
    gewog = Column(String(255), nullable=False)
    dzongkhag = Column(String(255), nullable=False)


class Directory(Base):
    __tablename__ = 'Directory'

    directoryid = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    hod = Column(ForeignKey('Staff.staffid'), unique=True)

    Staff = relationship('Staff', primaryjoin='Directory.hod == Staff.staffid')

    
class Institution(Base):
    __tablename__ = 'Institution'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    director = Column(String(255), nullable=False)


class Staff(Base):
    __tablename__ = 'Staff'

    staffid = Column(String(8), primary_key=True)
    cid = Column(String(11))
    name = Column(String(255), nullable=False)
    gender = Column(Enum('male', 'female', 'others'), nullable=False)
    nationality = Column(String(255), nullable=False)
    phonenumber = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    bloodgroup = Column(Enum('a+', 'a-', 'b+', 'b-', 'ab+', 'ab-', 'o+', 'o-'), nullable=False)
    dateofbirth = Column(Date, nullable=False)
    permanentaddress = Column(ForeignKey('Address.addressid'), index=True)
    temporaryaddress = Column(ForeignKey('Address.addressid'), index=True)
    salary = Column(DECIMAL(10, 2), nullable=False)
    joiningdate = Column(Date, nullable=False)
    staffstatus = Column(Enum('active', 'study_leave', 'resignation', 'suspended', 'deceased', 'retired', 'maternity_paternity_leave', 'medical_leave', 'on_leave', 'probationary'), nullable=False)
    positionlevel = Column(Integer, nullable=False)
    positiontitle = Column(String(255), nullable=False)
    stafftype = Column(Enum('academic', 'non_academic'), nullable=False)
    directoryid = Column(ForeignKey('Directory.directoryid'), index=True)
    image = Column(String(255))


    Directory = relationship('Directory', primaryjoin='Staff.directoryid == Directory.directoryid')
    Addres = relationship('Address', primaryjoin='Staff.permanentaddress == Address.addressid')
    Addres1 = relationship('Address', primaryjoin='Staff.temporaryaddress == Address.addressid')
    Training = relationship('Training', secondary='StaffTraining')


class Dependent(Base):
    __tablename__ = 'Dependent'

    number = Column(Integer, primary_key=True)
    cid = Column(String(11))
    name = Column(String(255), nullable=False)
    gender = Column(Enum('male', 'female', 'others'), nullable=False)
    phonenumber = Column(String(20), nullable=False)
    bloodgroup = Column(Enum('a+', 'a-', 'b+', 'b-', 'ab+', 'ab-', 'o+', 'o-'), nullable=False)
    dateofbirth = Column(Date, nullable=False)
    relationtype = Column(Enum('spouse', 'child', 'parent', 'sibling', 'other'), nullable=False)
    permanentaddress = Column(ForeignKey('Address.addressid'), nullable=False, index=True)
    temporaryaddress = Column(ForeignKey('Address.addressid'), nullable=False, index=True)
    staffid = Column(ForeignKey('Staff.staffid'), index=True)

    Addres = relationship('Address', primaryjoin='Dependent.permanentaddress == Address.addressid')
    Staff = relationship('Staff')
    Addres1 = relationship('Address', primaryjoin='Dependent.temporaryaddress == Address.addressid')


class Qualification(Base):
    __tablename__ = 'Qualification'

    id = Column(Integer, primary_key=True)
    institutionid = Column(ForeignKey('Institution.id'), index=True)
    name = Column(String(255), nullable=False)
    graduationdate = Column(Date, nullable=False)
    majorfield = Column(String(255), nullable=False)
    gpagrade = Column(DECIMAL(3, 2), nullable=False)
    honorsaward = Column(Enum('none', 'cum_laude', 'magna_cum_laude', 'summa_cum_laude'), nullable=False)
    staffid = Column(ForeignKey('Staff.staffid'), index=True)

    Institution = relationship('Institution')
    Staff = relationship('Staff')


class Training(Base):
    __tablename__ = 'Training'

    trainingid = Column(Integer, primary_key=True)
    institutionid = Column(ForeignKey('Institution.id'), index=True)
    name = Column(String(255), nullable=False)
    instructorname = Column(String(255), nullable=False)
    startingdate = Column(Date, nullable=False)
    endingdate = Column(Date, nullable=False)

    Institution = relationship('Institution')


t_StaffTraining = Table(
    'StaffTraining', metadata,
    Column('staffid', ForeignKey('Staff.staffid'), primary_key=True, nullable=False),
    Column('trainingid', ForeignKey('Training.trainingid'), primary_key=True, nullable=False, index=True)
)
